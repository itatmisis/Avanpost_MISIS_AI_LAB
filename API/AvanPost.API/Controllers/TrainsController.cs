using Avanpost.Data;
using AvanPost.API.Configuration;
using AvanPost.API.Models.Requests;
using AvanPost.API.RabbitMQ;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Options;
using System.Threading.Tasks;
using System;
using System.IO;

namespace AvanPost.API.Controllers
{


    [ApiController]
    [Route("[controller]")]
    public class TrainsController: ControllerBase
    {

        private readonly AvanpostContext _context;
        private readonly RabbitMQSendTrain _rabbitMqSendTrain;
        private const string DATASET_PATH = "default";
        private readonly AppSettings _appSettings;

        public TrainsController(AvanpostContext context, IOptions<AppSettings> options,  IOptions<RabbitMQConfig> rabbitMqConf, IOptions<AppSettings> settings)
        {
            _rabbitMqSendTrain = new RabbitMQSendTrain(rabbitMqConf.Value);
            _context = context;
            _appSettings = settings.Value;
        
        }

        [HttpPost("Train")]
        public async Task<ActionResult> Train(TrainRequest request)
        {

            foreach(var @class in request.Classes)
            {
                var _dbClass = await _context.DataClasses.FindAsync(@class);

                if(_dbClass != null)
                {
                    foreach (string newPath in Directory.GetFiles(Path.Combine(_appSettings.ImagesFolder, _dbClass.Name)))
                    {
                        System.IO.File.Copy(newPath, newPath.Replace(_appSettings.ImagesFolder, _appSettings.ToTrainImages), true);
                    }
                }
            }
            var key = Guid.NewGuid().ToString();

            var train = new Avanpost.Data.Entities.Train()
            {
                Key = key,
            };
            await _context.Trains.AddAsync(train);

            await _context.SaveChangesAsync();

            _rabbitMqSendTrain.Send(new RabbitMQ.Contracts.TrainMessage()
            {
                Key = key,
                DatasetPath = DATASET_PATH
            });

            while (train.Status != 2 || train.Status!= 3)
            {
                await Task.Delay(1000);
                train = await _context.Trains.FindAsync(train.Id);
            }

            return Ok(train);
        }
    }
}
