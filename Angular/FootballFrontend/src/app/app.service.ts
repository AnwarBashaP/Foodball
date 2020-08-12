import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { getLocaleExtraDayPeriodRules } from '@angular/common';
import { TouchSequence } from 'selenium-webdriver';
@Injectable({
  providedIn: 'root'
})
export class TournamentsService {

  // private _tournamentsurl = "http://205.147.97.85:5050/tournament/";
  private _tournamentsurl = "http://localhost:8000/api/";
  

 
  constructor(private http:HttpClient) {

   }

   getTournament(tourid)
   {
     return this.http.get<any>(this._tournamentsurl+'tourdetails/'+tourid+'/')
   }
    getTour()
    {
      // let headers = new HttpHeaders();
      // headers=headers.set('content-type','application/json')
      // headers=headers.set('Access-Control-Allow-Origin', '*');
      // let headers = new HttpHeaders().set('access-control-allow-origin',"http://localhost:8080/");
      return this.http.get<any>(this._tournamentsurl+'tourdetails/')
    }
    register(data)
    {
      return this.http.post<any>(this._tournamentsurl+'registertour/',{data})
    }
    getstatus()
    {
      return this.http.get<any>(this._tournamentsurl+'generate/')
    }
    matchstatusservice()
    {
      return this.http.get<any>(this._tournamentsurl+'generate/')
    }

}
