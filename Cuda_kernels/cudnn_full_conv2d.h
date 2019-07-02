#ifndef CUDNN_FULL_CONV2D_H
#define CUDNN_FULL_CONV2D_H

#include <cstddef>
#include <cudnn.h>

class CudnnConv2d
{

private:
  const size_t N;
  const size_t C;
  const size_t H;
  const size_t W;
  const size_t F;
  const size_t Y;
  const size_t X;

  void*                        d_workspace;
  cudnnHandle_t                cudnn;
  cudnnTensorDescriptor_t      input_descriptor;
  cudnnTensorDescriptor_t      output_descriptor;
  cudnnFilterDescriptor_t      kernel_descriptor;
  cudnnConvolutionDescriptor_t convolution_descriptor;
  cudnnConvolutionFwdAlgo_t    convolution_algorithm;
  size_t                       workspace_bytes = 0;

public:
  CudnnConv2d(const size_t N,
              const size_t C,
              const size_t H,
              const size_t W,
              const size_t F,
              const size_t Y,
              const size_t X);

  ~CudnnConv2d();

  void conv2d(float* U, float* K, float* V);
};

#endif /* CUDNN_FULL_CONV2D_H */