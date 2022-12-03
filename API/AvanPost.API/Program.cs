

using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Hosting;

namespace AvanPost.API
{

    public class Program
    {
        public static void Main(string[] args)
        {
            CreateHostBuilder(args).Build().Run();
        }

        public static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
                .ConfigureWebHostDefaults(webBuilder => {
                    webBuilder.UseStartup<Startup>()
                    .ConfigureKestrel(serverOptions =>
                    {
                    serverOptions.Limits.MaxRequestBodySize = 52428800 * 10;
                    });
                });
    }
}


