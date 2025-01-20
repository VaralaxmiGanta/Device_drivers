/home/vlab/qemu/build/qemu-system-x86_64 \
  --enable-kvm \
  -hda /home/vlab/x86/x86_image.qcow2 \
  -m 10G \
  -device tmp105,id=sensor,address=0x48 \
  -qmp unix:$HOME/qmp.sock,server,nowait \
  -nic user,hostfwd=tcp::2222-:22

