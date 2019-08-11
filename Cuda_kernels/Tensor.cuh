#ifndef TENSOR_H
#define TENSOR_H

#include <cstddef>
#include <initializer_list>
#include <memory>
#include <vector>


class Tensor
{
public:
  float*                m_data;
  std::vector<unsigned> shape;

  Tensor(std::initializer_list<unsigned>);
  Tensor(Tensor const&);
  Tensor(Tensor&&) = default;
  Tensor& operator =(Tensor const&);
  Tensor& operator=(Tensor&&) = default;
  ~Tensor();

  size_t size() const;
  size_t order() { return shape.size(); }
  /* float& operator[](size_t const index) { return m_data[index]; } */
};

#endif /* TENSOR_H */
