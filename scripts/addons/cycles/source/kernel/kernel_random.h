/*
 * Copyright 2011-2013 Blender Foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "kernel/kernel_jitter.h"

CCL_NAMESPACE_BEGIN

/* Pseudo random numbers, uncomment this for debugging correlations. Only run
 * this single threaded on a CPU for repeatable resutls. */
//#define __DEBUG_CORRELATION__


/* High Dimensional Sobol.
 *
 * Multidimensional sobol with generator matrices. Dimension 0 and 1 are equal
 * to classic Van der Corput and Sobol sequences. */

#ifdef __SOBOL__

/* Skip initial numbers that are not as well distributed, especially the
 * first sequence is just 0 everywhere, which can be problematic for e.g.
 * path termination.
 */
#define SOBOL_SKIP 64

ccl_device uint sobol_dimension(KernelGlobals *kg, int index, int dimension)
{
	uint result = 0;
	uint i = index;
	for(uint j = 0; i; i >>= 1, j++) {
		if(i & 1) {
			result ^= kernel_tex_fetch(__sobol_directions, 32*dimension + j);
		}
	}
	return result;
}

#endif /* __SOBOL__ */


ccl_device_forceinline float path_rng_1D(KernelGlobals *kg,
                                         RNG *rng,
                                         int sample, int num_samples,
                                         int dimension)
{
#ifdef __DEBUG_CORRELATION__
	return (float)drand48();
#endif

#ifdef __CMJ__
#  ifdef __SOBOL__
	if(kernel_data.integrator.sampling_pattern == SAMPLING_PATTERN_CMJ)
#  endif
	{
		/* Correlated multi-jitter. */
		int p = *rng + dimension;
		return cmj_sample_1D(sample, num_samples, p);
	}
#endif

#ifdef __SOBOL__
	/* Sobol sequence value using direction vectors. */
	uint result = sobol_dimension(kg, sample + SOBOL_SKIP, dimension);
	float r = (float)result * (1.0f/(float)0xFFFFFFFF);

	/* Cranly-Patterson rotation using rng seed */
	float shift;

	/* Hash rng with dimension to solve correlation issues.
	 * See T38710, T50116.
	 */
	RNG tmp_rng = cmj_hash_simple(dimension, *rng);
	shift = tmp_rng * (1.0f/(float)0xFFFFFFFF);

	return r + shift - floorf(r + shift);
#endif
}

ccl_device_forceinline void path_rng_2D(KernelGlobals *kg,
                                        RNG *rng,
                                        int sample, int num_samples,
                                        int dimension,
                                        float *fx, float *fy)
{
#ifdef __DEBUG_CORRELATION__
	*fx = (float)drand48();
	*fy = (float)drand48();
	return;
#endif

#ifdef __CMJ__
#  ifdef __SOBOL__
	if(kernel_data.integrator.sampling_pattern == SAMPLING_PATTERN_CMJ)
#  endif
	{
		/* Correlated multi-jitter. */
		int p = *rng + dimension;
		cmj_sample_2D(sample, num_samples, p, fx, fy);
		return;
	}
#endif

#ifdef __SOBOL__
	/* Sobol. */
	*fx = path_rng_1D(kg, rng, sample, num_samples, dimension);
	*fy = path_rng_1D(kg, rng, sample, num_samples, dimension + 1);
#endif
}

ccl_device_inline void path_rng_init(KernelGlobals *kg,
                                     ccl_global uint *rng_state,
                                     int sample, int num_samples,
                                     RNG *rng,
                                     int x, int y,
                                     float *fx, float *fy)
{
	/* load state */
	*rng = *rng_state;
	*rng ^= kernel_data.integrator.seed;

#ifdef __DEBUG_CORRELATION__
	srand48(*rng + sample);
#endif

	if(sample == 0) {
		*fx = 0.5f;
		*fy = 0.5f;
	}
	else {
		path_rng_2D(kg, rng, sample, num_samples, PRNG_FILTER_U, fx, fy);
	}
}

/* Linear Congruential Generator */

ccl_device uint lcg_step_uint(uint *rng)
{
	/* implicit mod 2^32 */
	*rng = (1103515245*(*rng) + 12345);
	return *rng;
}

ccl_device float lcg_step_float(uint *rng)
{
	/* implicit mod 2^32 */
	*rng = (1103515245*(*rng) + 12345);
	return (float)*rng * (1.0f/(float)0xFFFFFFFF);
}

ccl_device uint lcg_init(uint seed)
{
	uint rng = seed;
	lcg_step_uint(&rng);
	return rng;
}

/* Path Tracing Utility Functions
 *
 * For each random number in each step of the path we must have a unique
 * dimension to avoid using the same sequence twice.
 *
 * For branches in the path we must be careful not to reuse the same number
 * in a sequence and offset accordingly.
 */

ccl_device_inline float path_state_rng_1D(KernelGlobals *kg,
                                          RNG *rng,
                                          const ccl_addr_space PathState *state,
                                          int dimension)
{
	return path_rng_1D(kg,
	                   rng,
	                   state->sample, state->num_samples,
	                   state->rng_offset + dimension);
}

ccl_device_inline float path_state_rng_1D_for_decision(
        KernelGlobals *kg,
        RNG *rng,
        const ccl_addr_space PathState *state,
        int dimension)
{
	/* The rng_offset is not increased for transparent bounces. if we do then
	 * fully transparent objects can become subtly visible by the different
	 * sampling patterns used where the transparent object is.
	 *
	 * however for some random numbers that will determine if we next bounce
	 * is transparent we do need to increase the offset to avoid always making
	 * the same decision. */
	const int rng_offset = state->rng_offset + state->transparent_bounce * PRNG_BOUNCE_NUM;
	return path_rng_1D(kg,
	                   rng,
	                   state->sample, state->num_samples,
	                   rng_offset + dimension);
}

ccl_device_inline void path_state_rng_2D(KernelGlobals *kg,
                                         RNG *rng,
                                         const ccl_addr_space PathState *state,
                                         int dimension,
                                         float *fx, float *fy)
{
	path_rng_2D(kg,
	            rng,
	            state->sample, state->num_samples,
	            state->rng_offset + dimension,
	            fx, fy);
}

ccl_device_inline float path_branched_rng_1D(
        KernelGlobals *kg,
        RNG *rng,
        const ccl_addr_space PathState *state,
        int branch,
        int num_branches,
        int dimension)
{
	return path_rng_1D(kg,
	                   rng,
	                   state->sample * num_branches + branch,
	                   state->num_samples * num_branches,
	                   state->rng_offset + dimension);
}

ccl_device_inline float path_branched_rng_1D_for_decision(
        KernelGlobals *kg,
        RNG *rng,
        const ccl_addr_space PathState *state,
        int branch,
        int num_branches,
        int dimension)
{
	const int rng_offset = state->rng_offset + state->transparent_bounce * PRNG_BOUNCE_NUM;
	return path_rng_1D(kg,
	                   rng,
	                   state->sample * num_branches + branch,
	                   state->num_samples * num_branches,
	                   rng_offset + dimension);
}

ccl_device_inline void path_branched_rng_2D(
        KernelGlobals *kg,
        RNG *rng,
        const ccl_addr_space PathState *state,
        int branch,
        int num_branches,
        int dimension,
        float *fx, float *fy)
{
	path_rng_2D(kg,
	            rng,
	            state->sample * num_branches + branch,
	            state->num_samples * num_branches,
	            state->rng_offset + dimension,
	            fx, fy);
}

/* Utitility functions to get light termination value,
 * since it might not be needed in many cases.
 */
ccl_device_inline float path_state_rng_light_termination(
        KernelGlobals *kg,
        RNG *rng,
        const ccl_addr_space PathState *state)
{
	if(kernel_data.integrator.light_inv_rr_threshold > 0.0f) {
		return path_state_rng_1D_for_decision(kg, rng, state, PRNG_LIGHT_TERMINATE);
	}
	return 0.0f;
}

ccl_device_inline float path_branched_rng_light_termination(
        KernelGlobals *kg,
        RNG *rng,
        const ccl_addr_space PathState *state,
        int branch,
        int num_branches)
{
	if(kernel_data.integrator.light_inv_rr_threshold > 0.0f) {
		return path_branched_rng_1D_for_decision(kg,
		                                         rng,
		                                         state,
		                                         branch,
		                                         num_branches,
		                                         PRNG_LIGHT_TERMINATE);
	}
	return 0.0f;
}

ccl_device_inline void path_state_branch(ccl_addr_space PathState *state,
                                         int branch,
                                         int num_branches)
{
	/* path is splitting into a branch, adjust so that each branch
	 * still gets a unique sample from the same sequence */
	state->rng_offset += PRNG_BOUNCE_NUM;
	state->sample = state->sample*num_branches + branch;
	state->num_samples = state->num_samples*num_branches;
}

ccl_device_inline uint lcg_state_init(RNG *rng,
                                      int rng_offset,
                                      int sample,
                                      uint scramble)
{
	return lcg_init(*rng + rng_offset + sample*scramble);
}

ccl_device float lcg_step_float_addrspace(ccl_addr_space uint *rng)
{
	/* Implicit mod 2^32 */
	*rng = (1103515245*(*rng) + 12345);
	return (float)*rng * (1.0f/(float)0xFFFFFFFF);
}

CCL_NAMESPACE_END

