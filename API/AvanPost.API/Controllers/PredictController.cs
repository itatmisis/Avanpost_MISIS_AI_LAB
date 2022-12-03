using Avanpost.Data;
using Avanpost.Data.Entities;
using AvanPost.API.Configuration;
using AvanPost.API.RabbitMQ;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using System;
using System.Collections.Generic;
using System.IO;
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

            var keys = new List<string>();

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

                        keys.Add(key);


                    }
                }

                await _context.SaveChangesAsync();
                return Ok();
            }
            catch (Exception ex)
            {
                return BadRequest();
            }
        }
    }
}
