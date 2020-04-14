using System;
using System.IO;
using System.Net;
using System.Text;
using Newtonsoft.Json;


namespace ConsoleContester
{
    class Program
    {
        class Problem
        {
            public int id;
            public string mqtt_key;
            public string user;
            public string language;
            public string course;
            public int problem;
            public int variant;
            public string code;
        }


        static void Main(string[] args)
        {
            Problem problem = new Problem();
            problem.id = 5;
            problem.mqtt_key = "123";
            problem.course = "na";
            problem.user = "sinegordon";
            problem.language = "python3";
            problem.problem = 1;
            problem.variant = 1;
            problem.code = "print(input())";
            string json = JsonConvert.SerializeObject(problem);
            byte[] body = Encoding.UTF8.GetBytes(json);
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create("https://cloud.mst-dev.ru/contest/api/add_transaction");
            request.Method = "POST";
            request.ContentType = "application/json; charset=utf-8";
            request.ContentLength = body.Length;
            using (Stream stream = request.GetRequestStream())
            {
                stream.Write(body, 0, body.Length);
                stream.Close();
            }
            using (HttpWebResponse response = (HttpWebResponse)request.GetResponse())
            {
                response.Close();
            }
        }
    }
}
