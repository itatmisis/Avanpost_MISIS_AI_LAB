using AvanPost.API.RabbitMQ.Contracts;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using RabbitMQ.Client;
using AvanPost.API.Configuration;
using Microsoft.Extensions.Options;

namespace AvanPost.API.RabbitMQ
{
    public class RabbitMQSendPredict
    {

        private readonly ConnectionFactory _factory;
        private readonly string _queue;

        public RabbitMQSendPredict(RabbitMQConfig config)
        {
            var rabbitConfig = config;
        
            var factory = new ConnectionFactory();

            factory.UserName = rabbitConfig.UserName;
            factory.Password = rabbitConfig.Password;
            factory.VirtualHost = rabbitConfig.VirtualHost;
            factory.HostName = rabbitConfig.HostName;

            _queue = rabbitConfig.PredictQueue;
        }
        public  void Send(PredictMessage message)
        {

           

            using (var connection = _factory.CreateConnection())
            using (var channel = connection.CreateModel())
            {
                channel.QueueDeclare(queue: _queue,
                               durable: true,
                               exclusive: false,
                               autoDelete: false,
                               arguments: null);

                var body = Encoding.UTF8.GetBytes(JsonConvert.SerializeObject(message));

                channel.BasicPublish(exchange: "",
                               routingKey: _queue,
                               basicProperties: null,
                               body: body);
            }
        }
    }
}
