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

RUN git clone https://github.com/fuzzstati0n/fuzzgoat /src && \
  cd /src && \
  make

COPY layout.kdl /etc/zellij/layout.kdl
COPY run_nodes.py /src/run_nodes.py
COPY analyze.py /src/analyze.py

ENV SHELL="/usr/bin/bash"
CMD ["/usr/local/bin/zellij", "--layout", "/etc/zellij/layout.kdl"]
