
import gradio as gr

def click_fn(im1):
    print(f'image 1 clicked ')
with gr.Blocks() as demo:
    with gr.Row():
        im1= gr.Image(elem_id='tp',value ='Tanmay_Patil_thumbnail.png',label="resume1", height=100, width=50,scale=0)
        im2 = gr.Image(elem_id='ak',value ='Andrej_Karpathy_thumbnail.png',label="resume2", height=100, width=50,scale=0)

    
    
    

if __name__ == "__main__":
    demo.launch()