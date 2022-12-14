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
               var response =  await _parserApi.Send(new ParserApi.Models.ParserRequest()
                {
                    ClassName = request.ClassName,
                    FolderName = "/parseImages"
                });
                Console.WriteLine(response);

                if(response?.StatusCode == System.Net.HttpStatusCode.OK)
                {
                    return Ok(Directory.GetFiles($"//parseImages//{request.ClassName}").Select(x => Path.GetFileName(x)));
                }


                return BadRequest();
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                return BadRequest();
            }
        }
    }
}
