# Copyright (c) 2023 Habana Labs, Ltd. an Intel Company
# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: Apache-2.0

# DeepSpeed Team

from .builder import CPUOpBuilder


class CPUAdamBuilder(CPUOpBuilder):
    BUILD_VAR = "DS_BUILD_CPU_ADAM"
    NAME = "cpu_adam"

    def __init__(self):
        super().__init__(name=self.NAME)
        self.dtype = None

    def set_dtype(self, dtype):
        import torch
        assert (dtype in [torch.bfloat16, torch.half, torch.float32])
        self.dtype = dtype
        return self

    def absolute_name(self):
        return f'deepspeed.ops.adam.{self.NAME}_op'

    def sources(self):
        return ['csrc/adam/cpu_adam.cpp', 'csrc/adam/cpu_adam_impl.cpp']

    def cxx_args(self):
        import torch
        args = super().cxx_args()
        assert self.dtype is not None, "dype not set"
        if self.dtype == torch.bfloat16:
            args += ['-DHALF_DTYPE=c10::BFloat16']
        elif self.dtype == torch.half:
            args += ['-DHALF_DTYPE=c10::Half']
        else:
            args += ['-DHALF_DTYPE=float']
        return args

    def libraries_args(self):
        args = super().libraries_args()
        return args

    def include_paths(self):
        return ['csrc/includes']
