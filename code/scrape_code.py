from bs4 import BeautifulSoup
import requests
import time
import json
import random
import csv

next_page_urls = []
html = requests.get('https://www.doximity.com/directory/md/specialty/psychiatry').text
m = -1
q = 0
while m < 10000:
    soup_master = BeautifulSoup(html)
    soup_div = soup_master.find('ul', class_='list-4-col')

    doctor_hrefs = []
    for li in soup_div.find_all('li'):
        doctor_hrefs.append(li.a.get('href'))

    failed_urls = {}
    for i in range(len(doctor_hrefs)):
        m = m + 1
        dict_doctor = {}
        doctor_id = m

        time.sleep(random.uniform(0.5, 5))
        full_url = 'https://www.doximity.com' + doctor_hrefs[i]
        html = requests.get(full_url).text
        soup = BeautifulSoup(html)

        try:
            first_name_html = soup.find('span', class_='user-name-first')
            first_name = first_name_html.get_text() if first_name_html else None

            last_name_html = soup.find('span', class_='user-name-last')
            last_name = last_name_html.get_text() if last_name_html else None

            specialty_html = soup.find('a', class_='profile-head-subtitle')
            specialty = specialty_html.get_text() if specialty_html else None

            sub_specialty_html = soup.find('p', class_='user-subspecialty')
            sub_specialty = sub_specialty_html.get_text() if sub_specialty_html else None

            job_title_html = soup.find('p', class_='user-job-title')
            # job_title = job_title_html.get_text() if job_title_html else None
            job_titles = []
            if job_title_html:
                for line in job_title_html:
                    if line.string:
                        job_titles.extend(line.string.split('\n'))

            office_html = soup.find('span', class_='black profile-contact-labels-wrap')
            office = office_html.get_text() if office_html else None

            hosp_aff = soup.find('section', class_='hospital-info')
            hospitals_list = []
            if hosp_aff:
                hospitals = hosp_aff.find_all('span', class_='black', itemprop='name')
                
                for line in hospitals:
                    hospitals_list.append(line.string)

            awards_section = soup.find('section', class_='award-info')
            awards_list = []
            if awards_section:
                awards = awards_section.find_all('li', class_='show_more_hidden')
                # awarding_inst = awards_section.find_all('span', class_ = 'br')
                
                for line in awards:
                    awards_list.append(line.get_text())

            dict_doctor.update({doctor_id: {
                'url': full_url,
                'first_name': first_name,
                'last_name': last_name,
                'specialty': specialty,
                'sub_specialty': sub_specialty,
                'office': office,
                'job_titles': job_titles,
                'hospital': hospitals_list,
                'awards': awards_list,
                'training': {}
            }})
            training = soup.find('ul', class_='profile-sectioned-list training')
            institutions = training.find_all('span', class_='black')
            degrees = training.find_all('span', class_='br')

            if institutions:
                for j in range(len(institutions)):
                    dict_doctor[doctor_id]['training'][j] = {
                        institutions[j].get_text(): degrees[j].get_text().split(', ')}

        except Exception as e:
            dict_doctor[doctor_id] = str(e)
            dict_doctor[html] = html
            failed_urls[doctor_id] = full_url

        with open('/Users/nima/Desktop/PhD/NETS 5116/physician_trajectories/data/psychiatry/' + str(
                doctor_id) + '.json', 'w', encoding='utf-8') as f:
            json.dump(dict_doctor, f, ensure_ascii=False, indent=4)

        print(m)
        #clear_output(wait=True)

    with open('/Users/nima/Desktop/PhD/NETS 5116/physician_trajectories/data/psychiatry/failed_urls' + str(
            q) + '.json', 'w', encoding='utf-8') as f:
        json.dump(failed_urls, f, ensure_ascii=False, indent=4)
    q = q + 1

    if soup_master.find('a', class_='next_page'):
        next_href = soup_master.find('a', class_='next_page').get('href')
        next_url = 'https://www.doximity.com' + next_href
        next_page_urls.append(next_url)
        html = requests.get(next_url).text
    else:
        print('end reached')
        break

#print(next_page_urls)

with open('/Users/nima/Desktop/PhD/NETS 5116/physician_trajectories/data/psychiatry/next_page_urls.csv', 'w',
          newline='') as file:
    writer = csv.writer(file)
    # Write a header row if needed
    writer.writerow(["url"])
    # Write each string as a row
    for row in next_page_urls:
        writer.writerow([row])


# import socket
#
# hostname = socket.gethostname()
# IPAddr = socket.gethostbyname(hostname)
#
# print("Your Computer Name is: " + hostname)
# print("Your Computer IP Address is: " + IPAddr)
