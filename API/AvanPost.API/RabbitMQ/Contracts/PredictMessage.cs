using Newtonsoft.Json;

namespace AvanPost.API.RabbitMQ.Contracts
{
    public class PredictMessage
    {
        [JsonProperty(PropertyName ="key")]
        public string Key { get; set; }
        [JsonProperty(PropertyName = "image_filename")]

        public string ImageFileName { get; set; }
    }
}
