sudo apt install -y qemu-user-static binfmt-support
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
docker buildx create --name profile
docker buildx use profile
docker buildx inspect --bootstrap
