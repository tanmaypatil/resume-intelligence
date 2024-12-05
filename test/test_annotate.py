def test_annotate():
    annotate = []
    temp_annotate = [ "annotate1: pdf1","annotate 2 : pdf2"]
    annotate.extend(temp_annotate)
    temp_annotate2 = [ "annotate3: pdf3","annotate 4 : pdf4"]
    annotate.extend(temp_annotate2)
    print(f"annotate :  {annotate}")