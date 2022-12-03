using Avanpost.Data;
using Avanpost.Data.Entities;
using AvanPost.API.Configuration;
using AvanPost.API.Models.Requests;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Newtonsoft.Json;
using System;
using System.IO;
using System.Threading.Tasks;

namespace AvanPost.API.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class UploadImagesController : ControllerBase
    {


        private readonly ILogger<UploadImagesController> _logger;
        private readonly AvanpostContext _context;
        private readonly AppSettings _settings;

        public UploadImagesController(ILogger<UploadImagesController> logger, AvanpostContext context, IOptions<AppSettings> options)
        {
            _logger = logger;
            _context = context;
            _settings = options.Value;
        }

        [HttpPost(Name = "Upload")]
        public async Task<IActionResult> Upload()
        {
            var a = Request.Form["request"];

            var request = JsonConvert.DeserializeObject<CreateClassRequest>(Request.Form["request"]);

            if(request == null)
            {
                return BadRequest("Отсутствует request в FormData");
            }


            if (string.IsNullOrEmpty(request.ClassName))
            {
                return BadRequest("Название класса не может быть пустым");
            }

            var dataClass = new DataClass()
            {
                Name = request.ClassName
            };

            var imagesFolder = Path.Combine(_settings.ImagesFolder, dataClass.Name);

            if (!Directory.Exists(imagesFolder))
            {
                Directory.CreateDirectory(imagesFolder);
            }

            try
            {
                await _context.DataClasses.AddAsync(dataClass);
                await _context.SaveChangesAsync();

                var files = Request.Form.Files;

                foreach (var file in files)
                {
                    if (file.Length > 0)
                    {
                        var filePath = Path.Combine(imagesFolder, file.FileName);

                        using (var stream = System.IO.File.Create(filePath))
                        {
                            await file.CopyToAsync(stream);

                        }
                       await _context.Images.AddAsync(new Images()
                        {
                            Path = Path.Combine(dataClass.Name, file.FileName),
                            DataClassId = dataClass.Id
                        });
                    }
                }

                await _context.SaveChangesAsync();
                return Ok();
            }
            catch (Exception ex)
            {
                return BadRequest("Ошибка во время создания класса");
            }
        }
    }
}