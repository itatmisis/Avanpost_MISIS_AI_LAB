using AvanPost.API.Models.Requests;
using AvanPost.API.ParserApi;
using Microsoft.AspNetCore.Mvc;
using System;
using System.IO;
using System.Threading.Tasks;
using System.Linq;

namespace AvanPost.API.Controllers
{

    [ApiController]
    [Route("[controller]")]
    public class ParserController: ControllerBase
    {

        private readonly ParserApiCaller _parserApi;

        public ParserController()
        {
    
            _parserApi = new ParserApiCaller();
        }

        [HttpPost("Parse")]
        public async Task<ActionResult> Parse(ParseRequest request)
        {
            try
            {
                await _parserApi.Send(new ParserApi.Models.ParserRequest()
                {
                    ClassName = request.ClassName,
                    FolderName = "/ParserImages"
                });

                for(int i = 0; i < 10; i++)
                {
                    if (Directory.Exists(Path.Combine("/ParserImages", request.ClassName))){

                        var files = Directory.GetFiles(Path.Combine("/ParserImages", request.ClassName));
                        if (files.Any())
                        {
                            return Ok(files.Select(x => Path.GetFileName(x)));
                        }
                    }
                    await Task.Delay(1000);


                }
                return Ok(new string[] { });
            }
            catch (Exception ex)
            {
                return BadRequest();
            }
        }
    }
}
