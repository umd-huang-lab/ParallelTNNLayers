#if GOOGLE_CUDA
#define EIGEN_USE_GPU
/* #include "third_party/eigen3/unsupported/Eigen/CXX11/Tensor" */

__global__
void
AddOneKernel(const float* in, const int N, float* out) {
  for (int i = blockIdx.x * blockDim.x + threadIdx.x;
      i < N;
      i += blockDim.x * gridDim.x)
  {
    out[i] = in[i] + 1;
  }
}

void AddOneKernelLauncher(const float* in, const int N, float* out) {
  AddOneKernel<<<32, 256>>>(in, N, out);
}

#endif
