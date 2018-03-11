import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';


const API_URL = 'http://localhost:9000/api/';

@Injectable()
export class ApiService {

  constructor( private http: HttpClient ) { }

  public postMaker( endpoint, requestArgs ) {
    var url = API_URL + endpoint;

    return this.http.post( url, requestArgs );
  }

  private getMaker( endpoint, requestArgs ) {
    var url = API_URL + endpoint;

    return this.http.get( url, requestArgs );

  }

}
