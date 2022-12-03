using AvanPost.API.RabbitMQ.Contracts;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using RabbitMQ.Client;

namespace AvanPost.API.RabbitMQ
{
    public class RabbitMQSendPredict
    {
        public  void Send(PredictMessage message)
        {

            var factory = new ConnectionFactory();

            factory.UserName = "avanpostuser";
            factory.Password = "avanpostpassword";
            factory.VirtualHost = "/";
            factory.HostName = "213.178.155.140";

            using (var connection = factory.CreateConnection())
            using (var channel = connection.CreateModel())
            {
                channel.QueueDeclare(queue: "predict",
                               durable: true,
                               exclusive: false,
                               autoDelete: false,
                               arguments: null);

                var body = Encoding.UTF8.GetBytes(JsonConvert.SerializeObject(message));

                channel.BasicPublish(exchange: "",
                               routingKey: "predict",
                               basicProperties: null,
                               body: body);
            }
        }
    }
}
