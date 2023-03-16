import os
import pandas as pd
import googleapiclient.discovery
from googleapiclient import errors

# Antes de usar, você precisa de uma developer key do YT
DEVELOPER_KEY = "AIzaSyC-IGrurz9MApvHsM6WQ1BTtmVX7rnV9Co"


# Configuração API
def api_builder():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)
    return youtube


def video_extractor(api):
    next_page_token = ''
    videos = []
    while True:
        request = api.videos().list(
            part="id",
            chart="mostPopular",
            regionCode="BR",
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response["items"]:
            videos.append(item["id"])

        try:
            next_page_token = response["nextPageToken"]
        except KeyError:
            break
    return videos


def comments_extractor(api, videos):
    next_page_token = ''  # Para começar pela primeira pagina, este token deve ser nulo
    comments = []  # dar append comentário por comentário (sem suas respostas)
    for video_id in videos:
        print(f'{video_id}\n')
        while True:
            request = api.commentThreads().list(
                part="snippet",
                order="time",
                pageToken=next_page_token,
                videoId=video_id
            )
            try:
                response = request.execute()
            except errors.HttpError:
                break

            for item in response['items']:
                comments.append(item['snippet']['topLevelComment']['snippet']['textOriginal'])

            # Quando terminar de adicionar os comentários da página inicial(20), a API deve pegar o
            # token da próxima página, até que não tenha mais token (ou seja, quando der erro)
            try:
                next_page_token = response['nextPageToken']
            except KeyError:
                break
    return comments


def main():
    api = api_builder()
    videos = video_extractor(api)
    comments = comments_extractor(api, videos)

    print(f"{len(comments)} comentários")
    # Transforma a lista em DataFrame e disponibiliza o arquivo em csv
    df = pd.DataFrame(comments, columns=['Comentários'])
    df.to_csv("comentarios.csv", encoding='utf-8', index=False)


if __name__ == "__main__":
    main()





