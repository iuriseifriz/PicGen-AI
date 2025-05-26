import customtkinter as ctk
from PIL import Image, ImageTk
from gradio_client import Client
from tkinter.filedialog import asksaveasfilename

# UI config
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

client = Client("black-forest-labs/FLUX.1-dev")
generated_image = None

def generate_image():
    global generated_image
    prompt = prompt_entry.get()
    status_label.configure(text="Generating...", text_color="white")

    try:
        result = client.predict(
            prompt=prompt,
            seed=0,
            randomize_seed=True,
            width=1024,
            height=1024,
            guidance_scale=3.5,
            num_inference_steps=28,
            api_name="/infer"
        )

        image_path = result[0] if isinstance(result, (list, tuple)) else result
        generated_image = Image.open(image_path)
        preview = generated_image.resize((400, 400))
        tk_image = ImageTk.PhotoImage(preview)

        image_label.configure(image=tk_image, text="")
        image_label.image = tk_image
        status_label.configure(text="Image generated!", text_color="green")

    except Exception as e:
        status_label.configure(text=f"Error: {e}", text_color="red")

def download_image():
    if generated_image:
        file_path = asksaveasfilename(defaultextension=".png",
                                      filetypes=[("PNG files", "*.png")])
        if file_path:
            generated_image.save(file_path)
            status_label.configure(text="Image saved.", text_color="green")
    else:
        status_label.configure(text="No image to save.", text_color="orange")

# GUI layout
app = ctk.CTk()
app.title("PicGen - AI Image Generator")
app.geometry("520x700")

prompt_entry = ctk.CTkEntry(app, width=400, placeholder_text="Enter your prompt...")
prompt_entry.pack(pady=20)

generate_button = ctk.CTkButton(app, text="Generate Image", command=generate_image)
generate_button.pack(pady=10)

download_button = ctk.CTkButton(app, text="Download Image", command=download_image)
download_button.pack(pady=10)

status_label = ctk.CTkLabel(app, text="", text_color="white")
status_label.pack(pady=10)

image_label = ctk.CTkLabel(app, text="Image will appear here")
image_label.pack(pady=20)

credits = ctk.CTkLabel(app, text="Powered by FLUX.1-dev", text_color="gray")
credits.pack(pady=10)

app.mainloop()
