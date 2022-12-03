using Avanpost.Data;
using AvanPost.API.Configuration;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using System;
using System.Linq;
using System.Threading.Tasks;

namespace AvanPost.API.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class DataClassesController: ControllerBase
    {
        private readonly ILogger<DataClassesController> _logger;
        private readonly AvanpostContext _context;
        private readonly AppSettings _settings;

        public DataClassesController(ILogger<DataClassesController> logger, AvanpostContext context, IOptions<AppSettings> options)
        {
            _logger = logger;
            _context = context;
            _settings = options.Value;
        }

        [HttpGet("AllClasses")]
        public async Task<ActionResult> GetAllClasses()
        {
            try
            {
                var classes = _context.DataClasses
                    .Include(x => x.Images)
                    .ToList();

                return Ok(classes.Select(x => new
                {
                    x.Id,
                    x.Name,
                    Images = x.Images.Select(x => x.Path)
                }));
            }
            catch(Exception ex)
            {
                return BadRequest(ex.Message);
            }
        }
        
        [HttpGet("ClassesForTraining")]
        public ActionResult GetClassesForTraining()
        {
            try
            {
                var classes = _context.DataClasses
                     .Include(x => x.Images)
                    .Where(x => !x.ModelClasses.Any());

                return Ok(classes.Select(x => new
                {
                    x.Id,
                    x.Name,
                    Images = x.Images.Select(x => x.Path)
                }));
            }
            catch(Exception ex)
            {
                return BadRequest();
            }
        }
    }
}
