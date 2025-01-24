import pandas as pd
from parser_tools import (
    make_request,
    define_links,
    extract_info,
    save_file,
    read_txt
)


start_link = "https://xn--d1ai6ai.xn--p1ai"
# собираю весь каталог фирм женских духов в лист
fabric_links = read_txt("fabric_links.txt")

final_df = pd.DataFrame()
# итерируюсь по листу и собираю айтемы всех фирм в лист
for fabric_link in fabric_links:
    try:
        items_in_fabrik_html = make_request(start_link + fabric_link)
        items_in_fabrik_links = list(set(define_links(items_in_fabrik_html, fabric_link)))
        save_file("items_in_fabrik_links.txt", items_in_fabrik_links)
        items_in_fabrik_links = read_txt("items_in_fabrik_links.txt")
        # итерируюсь по айтемам и собираю инфу в дикт
        for items_in_fabrik_link in items_in_fabrik_links:
            fin_dict = {
                'company': items_in_fabrik_link.split('/')[-2],
                'name': items_in_fabrik_link.split('/')[-1]
            }
            try:
                item_html = make_request(start_link + items_in_fabrik_link)
            except:
                print(f"skip {items_in_fabrik_link}")
                continue
            try:
                item_row_list = item_html.find_all('div', attrs={'class': 'mb-1'})
                info_dict = extract_info(item_row_list)
                fin_dict.update(info_dict)
            except:
                print(f"skip {items_in_fabrik_link}")
                continue
            try:
                fin_dict['volume'] = item_html.find('td', attrs={'class': 'table_volume pl-2'}).find('span', attrs={'class': ''}).text.strip()
            except:
                fin_dict['volume'] = 0
            try:
                fin_dict['price'] = item_html.find('span', attrs={'itemprop':'price'}).text.strip()
            except:
                fin_dict['price'] = 0
            item_row = pd.DataFrame(fin_dict, index=[0])
            final_df = pd.concat([final_df, item_row], axis=0, ignore_index=True)
            final_df.to_csv('women_perfume.csv')
    except:
        print(f"skip {fabric_link}")
        continue
