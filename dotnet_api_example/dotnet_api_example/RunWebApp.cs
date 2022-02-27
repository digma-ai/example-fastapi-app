using System;
using OpenTelemetry.Trace;
using OpenTelemetry.Resources;
using OpenTelemetry.Metrics;
using OpenTelemetry.Instrumentation.Digma;
using OpenTelemetry;
using Microsoft.Extensions.DependencyInjection;

namespace dotnet_api_example;

public class RunWebApp
{

		public static void Run(string[] args)
        {

            var builder = WebApplication.CreateBuilder(args);

            // Add services to the container.

            builder.Services.AddControllers();
            // Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
            builder.Services.AddEndpointsApiExplorer();
            builder.Services.AddSwaggerGen();

            var serviceName = "example_dotnet_app";
            var serviceVersion = "1.0.0";
            var projectRoot = builder.Environment.ContentRootPath;
            var workingDirectory = System.IO.Path.GetDirectoryName(System.Reflection.Assembly.GetExecutingAssembly().Location);
            Console.WriteLine("project root: " + projectRoot);
            Console.WriteLine("workingDirectory: " + workingDirectory);

            string commitHash = "";
            string repositoryUrl = projectRoot + "/../../";
            if (LibGit2Sharp.Repository.IsValid(repositoryUrl))
            {
                commitHash = new LibGit2Sharp.Repository(repositoryUrl).Head.Tip.Sha;
            }

            builder.Services.AddOpenTelemetryTracing((builder) => builder
                    .AddAspNetCoreInstrumentation(options => {
                        options.RecordException = true;

                    }
                        )
                    .AddHttpClientInstrumentation()

                    .SetResourceBuilder(
                    ResourceBuilder.CreateDefault()
                        .AddService(serviceName: serviceName, serviceVersion: serviceVersion)
                        .AddDigmaAttributes(configure => { }))
                    .AddOtlpExporter(c => {
                        c.Endpoint = new Uri("http://localhost:5050");
                    })
                    .AddSource(serviceName)
                );
            var app = builder.Build();

            // Configure the HTTP request pipeline.
            if (app.Environment.IsDevelopment())
            {
                app.UseSwagger();
                app.UseSwaggerUI();
            }

            app.UseHttpsRedirection();

            app.UseAuthorization();

            app.MapControllers();

            app.Run();


        }
    
}

