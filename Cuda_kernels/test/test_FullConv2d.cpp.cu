#define DOCTEST_CONFIG_IMPLEMENTATION_IN_DLL
#include "../../external/doctest/doctest.h"
#include "../Tensor.cuh"
#include "../Utils.cuh"
#include "../FullConv2d.cuh"
#include "../NVConv2d.cuh"

TEST_CASE("Convolution test") {

  int x = 32;
  int c = 16;
  int k = 16;
  int n = 1;

  Tensor Input  = random_fill({ n, c, x, x }, 0, 1);
  Tensor Filter = random_fill({ k, c, 3, 3 }, 0, 1);

  auto Cudnn = NV::Conv2dForward(Input, Filter);

  REQUIRE(Input.size() == (n * c * x * x));
  REQUIRE(Input.shape[0] == n);
  REQUIRE(Input.shape[1] == c);
  REQUIRE(Input.shape[2] == x);
  REQUIRE(Input.shape[3] == x);

  auto Full_gpu = conv2d_full_gpu(Input, Filter, 1);

  REQUIRE(Cudnn.size() == Full_gpu.size());
  REQUIRE(Full_gpu.shape[0] == n);
  REQUIRE(Full_gpu.shape[1] == k);
  REQUIRE(Full_gpu.shape[2] == x);
  REQUIRE(Full_gpu.shape[3] == x);
  for (int i = 0; i < Cudnn.size(); ++i)
    REQUIRE(Cudnn.m_data[i]
            == doctest::Approx(Full_gpu.m_data[i]).epsilon(1e-5));
}