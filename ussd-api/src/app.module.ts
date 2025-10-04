import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { CacheModule } from '@nestjs/cache-manager';
import KeyvRedis from '@keyv/redis';
import { ClassRegistry } from './lib/class-registry';
import { StateService } from './services/state.service';
import { HomeHandler } from './handlers/home-handler';
import { HomeExitHandler } from './handlers/home-exit-handler';
import { PersonNameHandler } from './handlers/new-form/person-name-handler';
import { PersonNameExitHandler } from './handlers/new-form/person-name-exit-handler';
import { HospitalSelectHandler } from './handlers/new-form/hospital-select-handler';
import { CloseFormHandler } from './handlers/new-form/close-form-handler';
import { MedicalInsuranceHandler } from './handlers/new-form/medical-insurance-handler';
import { HospitalSelectExitHandler } from './handlers/new-form/hospital-select-exit-handler';

const redisUrl = process.env.REDIS_URL || 'redis://localhost:6379';
@Module({
  imports: [
    CacheModule.registerAsync({
      useFactory: async () => {
        return {
          stores: [
            new KeyvRedis(redisUrl),
          ],
        };
      },
    }),
  ],
  controllers: [AppController],
  providers: [AppService,StateService],
})
export class AppModule {
  constructor(private stateService: StateService) {
    // Register all handlers here using factories for DI
    ClassRegistry.registerMany({
      home: () => new HomeHandler(this.stateService),
      homeExit: () => new HomeExitHandler(this.stateService),
      personName  : () => new PersonNameHandler(this.stateService),
      personNameExit : () => new PersonNameExitHandler(this.stateService),
      hospitalSelect : () => new HospitalSelectHandler(this.stateService),
      hospitalSelectExit : () => new HospitalSelectExitHandler(this.stateService),
      closeForm : () => new CloseFormHandler(this.stateService),
      medicalInsurance : () => new MedicalInsuranceHandler(this.stateService),
      // Add more handlers here as needed
    });
  }
}
