sudo apt install -y qemu-user-static binfmt-support
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
docker buildx create --name sofia # name as you like
docker buildx use sofia
docker buildx inspect --bootstrap
