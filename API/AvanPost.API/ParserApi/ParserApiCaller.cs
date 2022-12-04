using AvanPost.API.ParserApi.Models;
using System.Net.Http;
using System.Threading.Tasks;
using System;

namespace AvanPost.API.ParserApi
{
    public class ParserApiCaller

    {
        private readonly HttpClient _client;

        public ParserApiCaller()
        {
            _client = new HttpClient();
        }
        public async Task<HttpResponseMessage> Send(ParserRequest request)
        {
           try{
                HttpRequestMessage message = new HttpRequestMessage()
                {
                    RequestUri = new System.Uri($"http://158.160.32.20:9000/get_images?object={request.ClassName}&folder_name={request.ClassName}&galery_name=default")
                };

                 return await _client.SendAsync(message);
           }
           catch(Exception ex){
                return null;
           }
          
        }
    }
}
