from PIL import Image

gif = Image.open("loading-gif.gif")

# Resize each frame and save
frames = []
for frame in range(gif.n_frames):
    gif.seek(frame)
    resized_frame = gif.copy().resize((50, 50))  # Resize to 200x200
    frames.append(resized_frame)

# Save the resized GIF
frames[0].save("resized_gif.gif", save_all=True, append_images=frames[1:])
