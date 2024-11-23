import gradio as gr



    

import gradio as gr

with gr.Blocks() as demo:
    table = gr.Dataframe([[1, 2, 3], [4, 5, 6]])
    gallery = gr.Gallery([("Tanmay_patil_thumbnail.png","Tanmay_Patil.pdf")])
    textbox = gr.Textbox("Hello World!")
    statement = gr.Textbox()

    def on_select( evt,second):
        print(type(evt))
        print(type(second))
        print(f"second {second}")
        return f" {evt[0]}"

    #table.select(on_select, table, statement)
    gallery.select(on_select, gallery, statement)
    #textbox.select(on_select, textbox, statement)

demo.launch()