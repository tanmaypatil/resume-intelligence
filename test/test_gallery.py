from file_util import list_files_with_extension

def test_list():
    list = list_files_with_extension(".\\resumes","png")
    list_gallery = [ (l,l.removesuffix("_thumbnail.png") + '.pdf') for l in list ]
    print(list_gallery)
    print(len(list_gallery))
