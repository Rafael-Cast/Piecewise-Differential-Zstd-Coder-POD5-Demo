FROM fedora:36 as build

WORKDIR /builder

COPY . .

RUN dnf install -y wget gcc-c++ gcc git make libarrow-devel-8.0.1
RUN mkdir -p ~/miniconda3
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
RUN bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
RUN rm -rf ~/miniconda3/miniconda.sh

RUN ~/miniconda3/bin/conda init bash && \
    source ~/.bashrc && \
    conda env create --file=env-docker.yaml && \
    conda activate PDZ && \
    bash build.sh init && \
    bash build.sh c clean release cmklog

RUN conda install libstdcxx-ng=12

ENTRYPOINT ["/builder/build/src/c++/copy"]

#FROM rockylinux:8.8 as run