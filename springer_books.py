from bs4 import BeautifulSoup
import requests
import PyPDF2, io, urllib3

http = urllib3.PoolManager()
res = requests.get('https://towardsdatascience.com/springer-has-released-65-machine-learning-and-data-books-for-free-961f8181f189');
med_html = BeautifulSoup(res.text, 'html.parser')
books_link = [i.attrs['href'] for i in med_html.find_all('a') if i.attrs['href'].find('link.springer.com')!=-1]
direct_download_links = []
print(len(books_link))
for i in range(len(books_link)):
    pdf_writer = PyPDF2.PdfFileWriter()
    springer_res = requests.get(books_link[i])
    springer_html = BeautifulSoup((springer_res.text),'html.parser')
    name = springer_html.find('h1').text
    link = 'https://link.springer.com'+springer_html.find_all(attrs= {'class':'test-bookpdf-link'})[0].attrs['href']
    direct_download_links.append(link)
    response = http.request('GET', link).data
    with io.BytesIO(response) as curr_pdf:
        read_pdf = PyPDF2.PdfFileReader(curr_pdf)
        num_pages = read_pdf.getNumPages()
        for j in range(num_pages):
            pdf_writer.addPage(read_pdf.getPage(j))
        with open(name+'.pdf','wb') as out:
            pdf_writer.write(out)
            out.close();