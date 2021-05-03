import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Subject} from 'rxjs';

@Injectable({providedIn: "root"})
export class AppService {
  clustersListener = new Subject<any>();
  isProcessingListener = new Subject<any>();
  clusters = [];

  constructor(private http: HttpClient) {}


  getClustersListener(){
    return this.clustersListener.asObservable();
  }

  getIsProcessingListener(){
    return this.isProcessingListener.asObservable();
  }

  getClusters(country, city){
    const queryString = `?country=${country}&city=${city.toLowerCase()}`;
    this.isProcessingListener.next(true);

    this.http.get<{clusters: [], status: number}>(`http://www.localhost:5000/${queryString}`).subscribe((resp) => {
      if(resp.status === 200){
        this.clusters = resp.clusters;
        this.clustersListener.next(this.clusters);

      } else {
            this.clustersListener.next([]);
        this.isProcessingListener.next(false);
      }


    })
  }

}
