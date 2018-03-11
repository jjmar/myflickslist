import { Component, OnInit } from '@angular/core';

import { ApiService } from './api.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'app';

  constructor( private apiService: ApiService ) {}

  ngOnInit() {
    console.log( 'Init of app component' );
    this.apiService.postMaker( 'auth/login', {} ).subscribe( resp => console.log( resp ) );

  }
}
