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

            };

            await _client.SendAsync(message);
          
        }
    }
}
