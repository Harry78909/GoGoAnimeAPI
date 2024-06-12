from bs4 import BeautifulSoup
import requests

class Gogoanime:
    def __init__(self, query=None, animeid=None, episode_num=None, genre_name=None, page=None):
        self.query = query
        self.animeid = animeid
        self.episode_num = episode_num
        self.genre_name = genre_name
        self.page = page

    @staticmethod
    def get_search_results(query):
        try:
            url = f"https://gogoanime.fi/search.html?keyword={query}"
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            animes = soup.find("ul", {"class": "items"}).find_all("li")
            
            res_list_search = []
            for anime in animes:
                title = anime.a["title"]
                url_path = anime.a["href"]
                anime_id = url_path.split('/')[2]
                res_list_search.append({"name": title, "animeid": anime_id})
            
            if not res_list_search:
                return {"status": "204", "reason": "No search results found for the query"}
            
            return res_list_search
        
        except requests.exceptions.ConnectionError:
            return {"status": "404", "reason": "Check the host's network Connection"}

    @staticmethod
    def get_anime_details(animeid):
        try:
            url = f'https://gogoanime.fi/category/{animeid}'
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")
            
            image_url = soup.find("div", {"class": "anime_info_body_bg"}).img.get('src')
            title = soup.find("div", {"class": "anime_info_body_bg"}).h1.string
            details = soup.find_all('p', {"class": "type"})
            
            plot_summary = details[1].get_text().split(':', 1)[1].strip()
            type_of_show = details[0].a['title']
            genres = [link.get('title') for link in details[2].find_all('a')]
            year = details[3].get_text().split(" ")[1]
            status = details[4].a.get_text()
            other_names = details[5].get_text().split(":", 1)[1].strip()
            last_episode = soup.find(id="episode_page").contents[-2].get_text().split("-")[-1]
            
            res_detail_search = {
                "title": title,
                "year": year,
                "other_names": other_names,
                "type": type_of_show,
                "status": status,
                "genre": genres,
                "episodes": last_episode,
                "image_url": image_url,
                "plot_summary": plot_summary
            }
            
            return res_detail_search
        
        except AttributeError:
            return {"status": "400", "reason": "Invalid animeid"}
        except requests.exceptions.ConnectionError:
            return {"status": "404", "reason": "Check the host's network Connection"}

    @staticmethod
    def get_episodes_link(animeid, episode_num):
        try:
            url = f'https://gogoanime.pe/{animeid}-episode-{episode_num}'
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")
            
            title = soup.find("div", {"class": "anime_info_body_bg"}).h1.string
            download_links = soup.find("li", {"class": "dowloads"}).a['href']
            download_response = requests.get(download_links)
            download_soup = BeautifulSoup(download_response.text, "lxml")
            download_items = download_soup.find_all('div', {'class': 'dowload'})
            
            episode_links = {'title': title}
            for item in download_items:
                quality = item.find('a').string.split()[1]
                link = item.find('a')['href']
                episode_links[quality] = link
            
            return episode_links
        
        except AttributeError:
            return {"status": "400", "reason": "Invalid animeid or episode_num"}
        except requests.exceptions.ConnectionError:
            return {"status": "404", "reason": "Check the host's network Connection"}

    @staticmethod
    def get_by_genre(genre_name, page):
        try:
            url = f"https://gogoanime.fi/genre/{genre_name}?page={page}"
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")
            
            animes = soup.find("ul", {"class": "items"}).find_all("li")
            genre_results = [{"genre": genre_name}]
            
            for anime in animes:
                title = anime.a["title"]
                anime_id = anime.a["href"].split('/')[2]
                genre_results.append({"title": title, "animeid": anime_id})
            
            return genre_results
        
        except (AttributeError, KeyError):
            return {"status": "400", "reason": "Invalid genre_name or page_num"}
        except requests.exceptions.ConnectionError:
            return {"status": "404", "reason": "Check the host's network Connection"}

# Example usage
#gogo = Gogoanime()

# Get search results
#search_results = gogo.get_search_results("Naruto")
#print(search_results)

# Get anime details
#anime_details = gogo.get_anime_details("naruto")
#print(anime_details)

# Get episode links
#episode_links = gogo.get_episodes_link("naruto", 1)
#print(episode_links)

# Get animes by genre
#animes_by_genre = gogo.get_by_genre("action", 1)
#print(animes_by_genre)
