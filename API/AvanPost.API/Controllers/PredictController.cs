using Avanpost.Data;
using Avanpost.Data.Entities;
using AvanPost.API.Configuration;
using AvanPost.API.Models.Response;
using AvanPost.API.RabbitMQ;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace AvanPost.API.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class PredictController : ControllerBase
    {

        private readonly string PREDICT_FOLDER = "Predict";
        private readonly ILogger<UploadImagesController> _logger;
        private readonly AvanpostContext _context;
        private readonly RabbitMQSendPredict _rabbitPredict;
        private readonly string _imageFolder;


        public PredictController(ILogger<UploadImagesController> logger, AvanpostContext context, IOptions<AppSettings> options)
        {
            _logger = logger;
            _context = context;
            _rabbitPredict = new RabbitMQSendPredict();
            _imageFolder = Path.Combine(options.Value.ImagesFolder, PREDICT_FOLDER);

            if (!Directory.Exists(_imageFolder))
            {
                Directory.CreateDirectory(_imageFolder);
            }
        }

        [HttpPost(Name ="Predict")]
        public async Task<ActionResult> Predict()
        {


            var files = Request.Form.Files;

            var keys = new List<Tuple<string, string>>();

            try
            {

                foreach (var file in files)
                {
                    if (file.Length > 0)
                    {
                        var filePath = Path.Combine(_imageFolder, file.FileName);

                        using (var stream = System.IO.File.Create(filePath))
                        {
                            await file.CopyToAsync(stream);

                        }
                        await _context.Images.AddAsync(new Images()
                        {
                            Path = Path.Combine(_imageFolder, file.FileName),
                        });

                        var key = Guid.NewGuid().ToString();

                        _rabbitPredict.Send(new RabbitMQ.Contracts.PredictMessage()
                        {
                            Key = key,
                            ImageFileName = file.FileName,
                        });

                        keys.Add(new Tuple<string, string>(key, file.FileName));


                    }
                }
                await _context.SaveChangesAsync();


                while (keys.Any())
                {
                    var predicts = new List<PredictResponse>();


                    var result = _context.Predicts.Where(x => keys.Select(x => x.Item1).Contains(x.Key));

                    predicts.AddRange(result.Select(x =>
                     new PredictResponse
                     {
                         Percent = x.Percent,
                         ClassName = x.ClassName,
                         FilaName = keys.FirstOrDefault(k => k.Item1 == x.Key).Item2
                     }));


                    keys = keys.Where(x => result.Select(y => y.Key).Contains(x.Item1)).ToList();
                }

                return Ok();
            }
            catch (Exception ex)
            {
                return BadRequest();
            }
        }
    }
}
