from django.db import models
from jsonfield import JSONField
import numpy as np
import random
import json
import io


class RNA(models.Model):
    FUNCAO_TRANSFERENCIA = (
        ('SG', 'Sigmóide'),
        ('EL', 'ELU'),
        ('RL', 'ReLU'),
        ('TH', 'Tangente Hiperbólica'),)

    INTERVALOS = (
        ('1', '(0, 1)'),
        ('2', '(-1, 0)'),
        ('3', '(-1, 1)'),
        ('4', '(-0.1, 0.1)'),)

    bias = models.BooleanField(default=False)
    funcao_transferencia = models.CharField(
        max_length=1, choices=FUNCAO_TRANSFERENCIA, default='SG')
    intervalo = models.CharField(
        max_length=1, choices=INTERVALOS, default='1')
    epoca = models.IntegerField(default=0)
    peso1 = JSONField()
    peso2 = JSONField()

    def sigmoid(self, soma):
        return 1 / (1 + np.exp(-soma))

    def sigmoidDerivate(self, sig):
        return sig * (1 - sig)

    def executar(self, testar=False):
        # iniciando valores
        neuronios = Neuronio.objects.filter(tipo='I')
        x1 = np.array([])
        x2 = np.array([])
        momento = 1
        taxa_aprendizagem = 0.5
        loop = 1

        # criando matrizes de entrada e saída
        for neuronio in neuronios:
            if round(neuronio.valor) == 1:
                x1 = np.append(x1, [[1]])
                x2 = np.append(x2, [[0]])
            else:
                x1 = np.append(x1, [[0]])
                x2 = np.append(x2, [[1]])
        entrada = np.vstack((x1, x2))
        saida_esperada = np.array([[1, 0],
                                  [0, 1]])

        # criando/pegando matrizes de peso
        self.peso1 = np.random.uniform(
            *eval(self.get_intervalo_display()),
            size=(13, 5)) if self.peso1 in 'None' else self.peso1
        self.peso2 = np.random.uniform(
            *eval(self.get_intervalo_display()),
            size=(5, 2)) if self.peso2 in 'None' else self.peso2
        if isinstance(self.peso1, str):
            memfile = io.BytesIO()
            memfile.write(json.loads(self.peso1).encode('latin-1'))
            memfile.seek(0)
            self.peso1 = np.load(memfile)
        if isinstance(self.peso2, str):
            memfile = io.BytesIO()
            memfile.write(json.loads(self.peso2).encode('latin-1'))
            memfile.seek(0)
            self.peso2 = np.load(memfile)

        # loop principal do treino
        if testar:
            loop = self.epoca
        for i in range(loop):
            # feed foward
            camada_entrada = entrada
            soma_sinapse0 = np.dot(camada_entrada, self.peso1)
            camada_hidden = self.sigmoid(soma_sinapse0)
            soma_sinapse1 = np.dot(camada_hidden, self.peso2)
            saida = self.sigmoid(soma_sinapse1)

            # calculando erro e codificando array
            erro = saida_esperada - saida
            media_absoluta = np.mean(np.abs(erro))
            print(media_absoluta)
            memfile = io.BytesIO()
            np.save(memfile, erro)
            memfile.seek(0)
            serialized = json.dumps(memfile.read().decode('latin-1'))
            e = Erro(valores=serialized, rna=self)
            e.save()

            # calculando descida do gradiente
            derivada_saida = self.sigmoidDerivate(saida)
            delta_saida = erro * derivada_saida

            # backpropagation
            delta_dot_peso = delta_saida.dot(self.peso2.T)
            camada_delta_hidden = delta_dot_peso * self.sigmoidDerivate(
                camada_hidden)

            # calculos de novos pesos
            novo_peso2 = camada_hidden.T.dot(delta_saida)
            self.peso2 = (self.peso2 * momento) + (novo_peso2 * taxa_aprendizagem)
            novo_peso1 = camada_entrada.T.dot(camada_delta_hidden)
            self.peso1 = (self.peso1 * momento) + (novo_peso1 * taxa_aprendizagem)

        print(saida)

        # salvando progresso dos pesos
        memfile = io.BytesIO()
        np.save(memfile, self.peso1)
        memfile.seek(0)
        self.peso1 = json.dumps(memfile.read().decode('latin-1'))
        memfile = io.BytesIO()
        np.save(memfile, self.peso2)
        memfile.seek(0)
        self.peso2 = json.dumps(memfile.read().decode('latin-1'))
        self.save()

    def __str__(self):
        return "({}, {}, {})".format(
            self.bias, self.funcao_transferencia, self.intervalo)


class Erro(models.Model):
    valores = JSONField()
    absolutos = JSONField()
    rna = models.ForeignKey(RNA, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)


class Neuronio(models.Model):
    TIPO = (
        ('I', 'Entrada'),
        ('H', 'Hidden'),
        ('O', 'Saída'),)

    rna = models.ForeignKey(RNA, on_delete=models.CASCADE)
    tipo = models.CharField(
        max_length=1, choices=TIPO, default='I')
    valor = models.DecimalField(max_digits=9, decimal_places=7)

    def create(self):
        self.valor = float('{0:.7f}'.format(
            random.uniform(*eval(self.rna.get_intervalo_display()))))

    def __str__(self):
        return '{} {}'.format(self.pk, self.valor)
