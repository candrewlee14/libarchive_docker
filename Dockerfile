FROM aflplusplus/aflplusplus

ARG TARGETPLATFORM
# install zellij
RUN if [ "$TARGETPLATFORM" = "linux/amd64" ]; then ARCHITECTURE=x86_64; elif [ "$TARGETPLATFORM" = "linux/arm/v7" ]; then ARCHITECTURE=arm; elif [ "$TARGETPLATFORM" = "linux/arm64" ]; then ARCHITECTURE=aarch64; else ARCHITECTURE=x86_64; fi && \
  apt-get update && \
  apt-get install -y curl && \
  curl -L "https://github.com/zellij-org/zellij/releases/latest/download/zellij-${ARCHITECTURE}-unknown-linux-musl.tar.gz" | tar xz && \
  mv zellij /usr/local/bin/ && \
  rm -rf zellij-* && \
  apt-get remove -y curl && \
  rm -rf /var/lib/apt/lists/*

# install htop
RUN apt-get update && \
  apt-get install -y htop && \
  rm -rf /var/lib/apt/lists/*

# RUN git clone https://github.com/fuzzstati0n/fuzzgoat /src && \
#   cd /src && \
#   make

ENV CC="afl-gcc"

RUN git clone https://github.com/libarchive/libarchive.git /src && \
  cd /src && \
  cmake . && \
  make

RUN cd /src && \
  git clone --depth=1 https://github.com/corkami/pocs && \
  mkdir seeds && \
  mv pocs/zip/*.zip ./seeds && \
  mv pocs/rar/*.rar ./seeds

ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/src/libarchive"

COPY layout.kdl /etc/zellij/layout.kdl
COPY run_nodes.py /src/run_nodes.py
COPY analyze.py /src/analyze.py

COPY fuzz_harness.cc /src/fuzz_harness.cc
RUN cd /src && \
  afl-g++ -o ./fuzz_harness fuzz_harness.cc -I/src/libarchive -L/src/libarchive -larchive -Wl,--trace 

ENV SHELL="/usr/bin/bash"
CMD ["/usr/local/bin/zellij", "--layout", "/etc/zellij/layout.kdl"]
