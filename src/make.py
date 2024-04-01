import tempfile
sprites = Path("./sprites")
frame_files = [f for f in sorted(os.listdir(sprites)) if f.startswith("frame")]

tempfiles = []
for file in frame_files:
    png_image = Image.open(sprites / file)
    with tempfile.NamedTemporaryFile(suffix=".webp", delete=False) as temp_file:
        # Save the image as WebP format
        png_image.save(temp_file.name, "WebP")
        tempfiles.append(temp_file.name +" +100")

# print(webpmux_animate(input_images=tempfiles, output_image="anim_container.webp",
#                       loop="10", bgcolor="255,255,255,255"))

frames = " ".join(f'-frame {f}' for f in tempfiles)
cmd = f"webpmux {frames} -loop 10 -bgcolor 255,255,255,255 -o out.webp"
print(cmd)

# webpmux  -frame /var/folders/3v/jl2nyhvx0fv2qfy6yz4fh9cw0000gn/T/tmp_bp7j2zq.webp +100 
#           -frame /var/folders/3v/jl2nyhvx0fv2qfy6yz4fh9cw0000gn/T/tmp2c4idylv.webp +100
#           -frame /var/folders/3v/jl2nyhvx0fv2qfy6yz4fh9cw0000gn/T/tmpx821h6zz.webp +100 
#           -loop 10 -bgcolor 255,255,255,255 -o anim_container.webp
