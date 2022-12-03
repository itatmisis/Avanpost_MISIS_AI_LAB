using Avanpost.Data;
using Avanpost.Data.Entities;
using AvanPost.API.Configuration;
using AvanPost.API.Models.Requests;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Newtonsoft.Json;
using System;
using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;
using AvanPost.API.ParserApi;

namespace AvanPost.API.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class UploadImagesController : ControllerBase
    {


        private readonly ILogger<UploadImagesController> _logger;
        private readonly AvanpostContext _context;
        private readonly AppSettings _settings;
        private readonly ParserApiCaller _parserApi;

        public UploadImagesController(ILogger<UploadImagesController> logger, AvanpostContext context, IOptions<AppSettings> options)
        {
            _logger = logger;
            _context = context;
            _settings = options.Value;
            _parserApi = new ParserApiCaller();
        }

        [HttpPost(Name = "Upload")]
        public async Task<IActionResult> Upload()
        {

            var request = JsonConvert.DeserializeObject<CreateClassRequest>(Request.Form["request"]);

            if(request == null)
            {
                return BadRequest("����������� request � FormData");
            }


            if (string.IsNullOrEmpty(request.ClassName))
            {
                return BadRequest("�������� ������ �� ����� ���� ������");
            }
            var files = Request.Form.Files;

            var dataClass = new DataClass()
            {
                Name = request.ClassName,
                SamplesNumber = files.Count
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

             

                foreach (var file in files)
                {
                    if (file.Length > 0)
                    {
                        var filePath = Path.Combine(imagesFolder, file.FileName);

                        Console.WriteLine(filePath);

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

                try
                {
                    await _parserApi.Send(new ParserApi.Models.ParserRequest()
                    {
                        ClassName = request.ClassName,
                        FolderName = "/ParserImages"
                    });
                }
                catch(Exception ex)
                {

                }


                return Ok();
            }
            catch (Exception ex)
            {
                return BadRequest("������ �� ����� �������� ������");
            }
        }
    }
}