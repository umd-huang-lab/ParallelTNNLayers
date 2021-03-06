import tensorflow as tf
import numpy as np
import os
import layers
import utils

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'


N=1
C=3
H=224
W=224
T=96
Y=11
X=11
rank=1

S=C



min_iters = 1024
padding = "SAME"
data_format = 'NCHW'

U = np.random.uniform(size=(N,C,H,W)).astype(np.float32)
K = np.random.uniform(size=(Y,X,S,T)).astype(np.float32)

kernel_size, kernel_size, input_filters, output_filters = K.shape

# params = layers.generate_params_conv2d_cp(input_filters, output_filters, kernel_size, rate)
params = {"rank" : rank}

factors = utils.factorize_conv2d_cp(K, params)

cp_kernels = {}
cp_kernels["kernel_0"] = factors[0]
cp_kernels["kernel_1"] = factors[1]
cp_kernels["kernel_2"] = factors[2]
K0 = factors[0].reshape(S,rank)
K1 = factors[1].reshape(Y,X,rank)
K2 = factors[2].reshape(rank,T)

Kcp = utils.recompose_conv2d_cp(factors, params)
normal_kernel = {"kernel" : Kcp}


if __name__ == "__main__":

    CPbench = tf.test.Benchmark()
    # cp_op_module = tf.load_op_library('../Kernels/cp_fused_nchw.so')

    with tf.Session() as sess:
        with tf.device('/device:XLA_GPU:0'):

            # Original operation from Su et al.
            V_orig = layers.conv2d_cp(U, cp_kernels, data_format=data_format)
            CPbench.run_op_benchmark(sess, V_orig, name='TF_original_cp_op', min_iters=min_iters)

            # # Custom fused GPU implementation.
            # V_fused = cp_op_module.conv2d_cp_fused_nchw(U,
            #         K0.reshape(16,6),
            #         K1.reshape(3,3,6),
            #         K2.reshape(6,16))
            # CPbench.run_op_benchmark(sess, V_fused, name='custom_fused_op', min_iters=min_iters)


            # # Sequencer operation
            # tU = tf.convert_to_tensor(U)
            # tK0 = tf.convert_to_tensor(K0)
            # tK1 = tf.convert_to_tensor(K1)
            # tK2 = tf.convert_to_tensor(K2)

            # V_seq_k3 = tf.einsum('hwr,rc->hwrc', tK1, tK2)
            # V_seq_u0 = tf.einsum('nchw,cr->nrhw', tU, tK0)
            # V_seq = tf.nn.conv2d(V_seq_u0, V_seq_k3, strides=[1,1,1,1], padding="SAME", data_format=data_format)
            # CPbench.run_op_benchmark(sess, V_seq, name='sequencer_nchw_op', min_iters=min_iters)

            # V_seq_k3_nhwc = tf.einsum('hwr,rc->hwrc', tK1, tK2)
            # V_seq_u0_nhwc = tf.einsum('nhwc,cr->nhwr', tf.transpose(tU, (0,2,3,1)) , tK0)
            # V_seq_nhwc = tf.nn.conv2d(V_seq_u0_nhwc, V_seq_k3_nhwc, strides=[1,1,1,1], padding="SAME")
            # CPbench.run_op_benchmark(sess, V_seq_nhwc, name='sequencer_nhwc_op', min_iters=min_iters)

            # # Rebuild Op.
            # V_rebuild = tf.einsum('ir,hwr,ro->hwio', tK0, tK1, tK2)
            # V_rebuild = tf.nn.conv2d(tU, V_rebuild, strides=[1,1,1,1], padding="SAME", data_format=data_format)
            # CPbench.run_op_benchmark(sess, V_rebuild, name='TF_rebuild_nchw_op', min_iters=min_iters)

            # # The full-sized kernel operation nchw
            # V_normal = layers.conv2d(U, normal_kernel, data_format=data_format)
            # CPbench.run_op_benchmark(sess, V_normal, name='TF_normal_nchw_op', min_iters=min_iters)

            # # The full-sized kernel operation nhwc
            # V_normal_nhwc = layers.conv2d(tf.transpose(U, (0,2,3,1)), normal_kernel, data_format='NHWC')
            # CPbench.run_op_benchmark(sess, V_normal, name='TF_normal_nhwc_op', min_iters=min_iters)
