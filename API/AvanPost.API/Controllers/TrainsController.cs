using Avanpost.Data;
using AvanPost.API.Configuration;
using AvanPost.API.Models.Requests;
using AvanPost.API.RabbitMQ;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using System.Threading.Tasks;
using System;

namespace AvanPost.API.Controllers
{


    [ApiController]
    [Route("[controller]")]
    public class TrainsController: ControllerBase
    {

        private readonly AvanpostContext _context;
        private readonly RabbitMQSendTrain _rabbitMqSendTrain;
        private const string DATASET_PATH = "default";

        public TrainsController(AvanpostContext context, IOptions<AppSettings> options,  IOptions<RabbitMQConfig> rabbitMqConf)
        {
            _rabbitMqSendTrain = new RabbitMQSendTrain(rabbitMqConf.Value);
            _context = context;
        
        }

        [HttpPost("Train")]
        public async Task Train(TrainRequest request)
        {
            var key = Guid.NewGuid().ToString();

            await _context.Trains.AddAsync(new Avanpost.Data.Entities.Train()
            {
                Key = key,
            });

            await _context.SaveChangesAsync();

            _rabbitMqSendTrain.Send(new RabbitMQ.Contracts.TrainMessage()
            {
                Key = key,
                DatasetPath = DATASET_PATH
            });
        }
    }
}
