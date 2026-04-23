from fpdf import FPDF
import lorem
import random
import string

def main():
    text = lorem.text()
    filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    filename = f"{filename}.pdf"
    pdf = FPDF()
    pdf.add_page()

    pdf.image("../images/Pfizer_Logo.png", w=40, keep_aspect_ratio=True)
    pdf.set_font("Times", size=12)

    pdf.set_x(10)
    pdf.set_font("Helvetica", style='B', size=16)
    pdf.multi_cell(0, 10, align='L', text='Discussion')
    pdf.set_x(10)
    pdf.set_font("Times", size=12)
    pdf.multi_cell(0, 5, text=text)


    # pdf.set_font("Times", size=12)
    # pdf.write(text=text, h=5)
    #    pdf.cell(200, 10, txt=text, ln=True, align='C')
    pdf.output(f"results/{filename}")
    print(f"Wrote pdf file {filename}")

if __name__ == '__main__':
    main()

