FROM ghcr.io/railwayapp/nixpacks:ubuntu-1690243402

ENTRYPOINT ["/bin/bash", "-l", "-c"]
WORKDIR /app/


COPY .nixpacks/nixpkgs-293a28df6d7ff3dec1e61e37cc4ee6e6c0fb0847.nix .nixpacks/nixpkgs-293a28df6d7ff3dec1e61e37cc4ee6e6c0fb0847.nix
RUN nix-env -if .nixpacks/nixpkgs-293a28df6d7ff3dec1e61e37cc4ee6e6c0fb0847.nix && nix-collect-garbage -d


ARG NIXPACKS_METADATA PYTHONUNBUFFERED
ENV NIXPACKS_METADATA=$NIXPACKS_METADATA PYTHONUNBUFFERED=$PYTHONUNBUFFERED

# setup phase
# noop

# install phase
# noop

# build phase
COPY . /app/.
RUN  pip install -r requirements.txt&&alembic upgrade head





# start
COPY . /app
CMD ["python main.py"]

