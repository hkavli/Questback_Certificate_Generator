import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib import utils
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Frame, Image

# Globale konstanter
WIL = "Wilhelm Hødnebø"
HAK = "Håkon Kavli"
QB = "Questback AS"
NAM = "Nordic Academy Manager"
HSA = "Head of Support and Training"


halvAnnenCM = cm
x = 0
# signaturer
# will:

# Norske beskjeder


# Variable
dato = datetime.now()
today = dato.strftime("%d.%m.%Y")


# basefarger
hexBaseBlaa = "#315665"
hexBaseGraa = "#919191"
hexBaseGroenn = "#74b5a5"

# aksentfarger
hexGraa = "#e8e6df"
hexBlaa = "#709bb6"
hexRoed = "#fd8770"
hexGul = "#feca79"
hexGroenn = "#2bcb75"
hexSvart = "#000000"
hexHvit = "#ffffff"

# Scale the logo for maintaining its proportions


def get_image(path, width):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))


def generate_diploma(attestID, navn, firmanavn, kursnavn, kursdato, kurssted, pdf_filename, navnASCII):
    attestID += 1
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    width = A4[0]
    height = A4[1]
    frame = Frame(0, 0, width, height-2*cm, showBoundary=False)
    c.setFillColor(HexColor(hexBaseBlaa))
    b = c.beginPath()
    b.moveTo(x, x)
    b.lineTo(x, height)
    b.lineTo(width, height)
    b.lineTo(width, x)
    c.drawPath(b, True, True)
    c.drawImage('img/questback_mark.png', 5, (height/4),
                width=(1776/3), height=(1182/3), mask='auto')
    c.setStrokeColor(HexColor(hexHvit))
    c.setFillColor(HexColor(hexHvit))
    c.setFont('Helvetica-Bold', 52, leading=True)
    c.drawCentredString((width/2), 675, 'academy')
    c.setFont('Helvetica', 52, leading=True)
    if kurssted == "Oslo" or kurssted == "Trondheim":
        c.setFont('Helvetica', 52, leading=True)
        c.drawCentredString((width/2), 550, 'Kursbevis')
        c.setFont('Helvetica-Bold', 34, leading=False)
        c.drawCentredString((width/2), 450, navn.encode())
        c.setFont('Helvetica', 24, leading=False)
        c.drawCentredString((width/2), 500, 'tildeles')
        c.drawCentredString((width/2), 400, "fra " + firmanavn)
        c.drawCentredString((width/2), 325, "For deltakelse på " + kursnavn)
        c.drawCentredString((width/2), 275, kurssted + ", " + kursdato)
        c.setFont('Helvetica', 18, leading=False)
        c.drawCentredString((width/4), 100, WIL)
        c.drawCentredString((width/4), 75, HSA)
        c.drawCentredString((width/4), 50, today)
        c.drawCentredString((width/4)*3, 100, HAK)
        c.drawCentredString((width/4)*3, 75, NAM)
        c.drawCentredString((width/4)*3, 50, today)
    elif kurssted == "Stockholm":
        c.setFont('Helvetica', 52, leading=True)
        c.drawCentredString((width/2), 550, 'Kursbevis')
        c.setFont('Helvetica-Bold', 34, leading=False)
        c.drawCentredString((width/2), 450, navn)
        c.setFont('Helvetica', 24, leading=False)
        c.drawCentredString((width/2), 500, 'tilldelas')
        c.drawCentredString((width/2), 400, "från " + firmanavn)
        c.drawCentredString((width/2), 325, "För deltagande på " + kursnavn)
        c.drawCentredString((width/2), 275, kurssted + ", " + kursdato)
        c.setFont('Helvetica', 18, leading=False)
        c.drawCentredString((width/4), 100, WIL)
        c.drawCentredString((width/4), 75, HSA)
        c.drawCentredString((width/4), 50, today)
        c.drawCentredString((width/4)*3, 100, HAK)
        c.drawCentredString((width/4)*3, 75, NAM)
        c.drawCentredString((width/4)*3, 50, today)

    # tegner strek under signaturer
    c.setLineJoin(mode=2)
    c.setLineWidth(1)
    p = c.beginPath()
    p.moveTo(50, 122)
    p.lineTo(250, 122)
    p.close()
    p.moveTo(350, 122)
    p.lineTo(550, 122)
    p.close()
    c.drawPath(p, fill=1, stroke=1)

    # signaturer
    # https://onlinepngtools.com/create-transparent-png
    c.drawImage('img/wilhelm.png', 50, 110, width=200,
                height=100, mask=[0, 0, 0, 0, 0, 0])
    c.drawImage('img/hakon.png', 350, 110, width=200,
                height=100, mask=[0, 0, 0, 0, 0, 0])
    story = []
    story.append(get_image('img/questback_white.png', width=width/1.25))
    frame.addFromList(story, c)
    c.showPage()
    c.save()

    os.path.join("/archive", pdf_filename, "w")

    print(f"Diplom for {navnASCII} er generert")
    return attestID
