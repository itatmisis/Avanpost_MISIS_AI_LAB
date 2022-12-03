using AvanPost.API.ParserApi.Models;
using System.Net.Http;
using System.Threading.Tasks;

namespace AvanPost.API.ParserApi
{
    public class ParserApiCaller

    {
        private readonly HttpClient _client;

        public ParserApiCaller()
        {
            _client = new HttpClient();
        }
        public async Task Send(ParserRequest request)
        {
            HttpRequestMessage message = new HttpRequestMessage()
            {
                RequestUri = new System.Uri($"http://158.160.32.20:9000/getImages?object={request.ClassName}&folder_name={request.FolderName}&galery_name={request.ClassName}")
            };

            await _client.SendAsync(message);
          
        }
    }
}
