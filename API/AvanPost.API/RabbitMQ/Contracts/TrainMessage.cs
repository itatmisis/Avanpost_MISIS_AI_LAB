using Newtonsoft.Json;

namespace AvanPost.API.RabbitMQ.Contracts
{
    public class TrainMessage
    {
        [JsonProperty("key")]
        public string Key { get; set; }
        [JsonProperty("dataset_path")]
        public string DatasetPath { get; set; }
    }
}
