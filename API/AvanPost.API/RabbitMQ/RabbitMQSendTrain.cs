using AvanPost.API.Configuration;
using AvanPost.API.RabbitMQ.Contracts;
using Microsoft.Extensions.Options;
using Newtonsoft.Json;
using RabbitMQ.Client;
using System.Text;

namespace AvanPost.API.RabbitMQ
{
    public class RabbitMQSendTrain
    {

        private readonly ConnectionFactory _factory;
        private readonly string _queue;

        public RabbitMQSendTrain(RabbitMQConfig config)
        {
            var rabbitConfig = config;

            _factory = new ConnectionFactory();

            _factory.UserName = rabbitConfig.UserName;
            _factory.Password = rabbitConfig.Password;
            _factory.VirtualHost = rabbitConfig.VirtualHost;
            _factory.HostName = rabbitConfig.HostName;

            _queue = rabbitConfig.TrainQueue;
        }
        public void Send(TrainMessage message)
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
