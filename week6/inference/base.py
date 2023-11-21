from abc import ABC

# 추상 클래스 생성
class Predictor(ABC): 
    @abstractmethod
    # Predictor Class 를 상속받은 대상은 무조건 그 안에서 load_model 은 구현해내야 한다.
    def load_model(model_path: str): # 모델 불러오기
        pass
    
    @abstractmethod
    def predict(input): # 모델 예측
        pass